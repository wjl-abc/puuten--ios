//
//  ViewController.m
//  puuten
//
//  Created by wang jialei on 12-7-25.
//  Copyright (c) 2012年 __MyCompanyName__. All rights reserved.
//

#import "ViewController.h"
#import "LoginViewController.h"
#import "ImageViewCell.h"
#import "WBViewController.h"
#import "BSHeader.h"
@interface ViewController () <LoginViewControllerDelegate, ImageViewCellDelegate>
@property (assign) BOOL login_or_not;
@end

@implementation ViewController
@synthesize login_or_not;

- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    if ([segue.identifier isEqualToString:@"login"]) {
        LoginViewController *login = (LoginViewController *)segue.destinationViewController;
        //login.email = @"email";
        //login.password = @"password";
        login.delegate = self;
    }
    if ([segue.identifier isEqualToString:@"detail"]){
        WBViewController *wb = (WBViewController *)segue.destinationViewController;
        wb.wb_id=selected_cell;
        wb.arrayImg = arrayImg;
        wb.order = selected_order;
        //BSHeader *bs = [[BSHeader alloc] init];
        //wb.name_string = @"mmmmm";
        //wb.url_string = @"http://tp2.sinaimg.cn/2105912065/180/5619589260/0";
        //wb.bsheader.name = @"mmmmm";
        //wb.bsheader.avatar_url = @"http://tp2.sinaimg.cn/2105912065/180/5619589260/0";
        //[wb.view addSubview:bs];
        
    }
}

- (void)didReceiveMemoryWarning
{
    // Releases the view if it doesn't have a superview.
    [super didReceiveMemoryWarning];
    
    // Release any cached data, images, etc that aren't in use.
}

#pragma mark - View lifecycle

- (void)loadInternetData {
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *libURL = [NSURL URLWithString:@"/home/" relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:libURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        NSMutableArray* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        arrayData = json;
        [self dataSourceDidLoad];
    }];
    [request setFailedBlock:^{
        [self dataSourceDidError];
    }];
    
    [request startAsynchronous];
   
}

- (void)dataSourceDidLoad {
    [waterFlow reloadData];
}

- (void)dataSourceDidError {
    [waterFlow reloadData];
}

- (id)initWithCoder:(NSCoder *)aDecoder
{
    if ((self = [super initWithCoder:aDecoder])) {
        self.navigationController.title = @"home";
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
	self.navigationController.title = @"home";
}

-(void)loadMore{
    
    [arrayData addObjectsFromArray:arrayData];
    [waterFlow reloadData];
}

#pragma mark WaterFlowViewDataSource
- (NSInteger)numberOfColumsInWaterFlowView:(WaterFlowView *)waterFlowView{
    
    return 2;
}

- (NSInteger)numberOfAllWaterFlowView:(WaterFlowView *)waterFlowView{
    
    return [arrayData count];
}

- (UIView *)waterFlowView:(WaterFlowView *)waterFlowView cellForRowAtIndexPath:(IndexPath *)indexPath{
    
    ImageViewCell *view = [[ImageViewCell alloc] initWithIdentifier:nil];
    
    return view;
}


-(void)waterFlowView:(WaterFlowView *)waterFlowView  relayoutCellSubview:(UIView *)view withIndexPath:(IndexPath *)indexPath{
    
    //arrIndex是某个数据在总数组中的索引
    int arrIndex = indexPath.row * waterFlowView.columnCount + indexPath.column;
    
    
    NSDictionary *object = [arrayData objectAtIndex:arrIndex];
    
    NSURL *nsURL = [[NSURL alloc] initWithString:[object objectForKey:@"thumbnail_pic"]];
    int wb_id = [[object objectForKey:@"wb_id"] intValue];
    int type = [[object objectForKey:@"type"] intValue];
    NSString *bsName = [object objectForKey:@"name"];
    NSString *name = [object objectForKey:@"user_name"];
    NSString *partnerName = [object objectForKey:@"partner"];
    NSString *info;
    ImageViewCell *imageViewCell = (ImageViewCell *)view;
    imageViewCell.indexPath = indexPath;
    imageViewCell.columnCount = waterFlowView.columnCount;
    imageViewCell.tt=0;
    [imageViewCell relayoutViews];
    switch (type) {
        case 1:
            info = @"把该信息加入了愿望单";
            break;
        case 2:
            info = @"更新了和该信息相关的活动专辑";
            break;
        case 4:
            info = [NSString stringWithFormat:@"接受了%@参加相关活动的邀请", partnerName];
        default:
            break;
    }
    NSData *data = [[NSData alloc] initWithContentsOfURL:nsURL];
    UIImage *image = [[UIImage alloc] initWithData:data];
    [arrayImg addObject:image];
    [(ImageViewCell *)view setImageWithImg:image withWB_ID:wb_id withOrder:arrIndex withBS:bsName withType:type withAvatar:nsURL withName:name withInfo:info withDelegate:self];
}


#pragma mark WaterFlowViewDelegate
- (CGFloat)waterFlowView:(WaterFlowView *)waterFlowView heightForRowAtIndexPath:(IndexPath *)indexPath{
    
    int arrIndex = indexPath.row * waterFlowView.columnCount + indexPath.column;
    NSDictionary *dict = [arrayData objectAtIndex:arrIndex];
    float height_width_ratio = [[dict objectForKey:@"ratio"] floatValue];
    return waterFlowView.cellWidth*height_width_ratio+58;
}

- (void)waterFlowView:(WaterFlowView * )waterFlowView didSelectRowAtIndexPath:(IndexPath *)indexPath{
    
    NSLog(@"indexpath row == %d,column == %d",indexPath.row,indexPath.column);
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}
- (void)viewDidAppear:(BOOL)animated
{
    if (!login_or_not) {
        [self performSegueWithIdentifier:@"login" sender:self];
    }
    else {
        //self.navigationController.title = @"home";
        arrayData = [[NSMutableArray alloc] init];
        self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"More" style:UIBarButtonItemStyleBordered target:self action:@selector(loadMore)];
        
        waterFlow = [[WaterFlowView alloc] initWithFrame:CGRectMake(0, 0, 320, 460-44)];
        waterFlow.waterFlowViewDelegate = self;
        waterFlow.waterFlowViewDatasource = self;
        waterFlow.backgroundColor = [UIColor whiteColor];
        [self.view addSubview:waterFlow];
        
        [self loadInternetData];
    }
    [super viewDidAppear:animated];
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation != UIInterfaceOrientationPortraitUpsideDown);
}

- (void)loginViewController:(LoginViewController *)sender 
               login_or_not:(int)userid
{
    self.login_or_not = YES;
    [self dismissModalViewControllerAnimated:YES];
}
/*
- (void)imageViewCell:(ImageViewCell *)sender
          clickedCell:(int)cell_id
{
    selected_cell = cell_id;
    [self performSegueWithIdentifier:@"detail" sender:self];
}*/

- (void)imageViewCell:(ImageViewCell *)sender
          clickedCell:(int)cell_id
         clickedOrder:(int)cell_order
{
    selected_cell = cell_id;
    selected_order = cell_order;
    [self performSegueWithIdentifier:@"detail" sender:self];
}

@end
