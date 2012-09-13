//
//  WBViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-3.
//
//

#import "WBViewController.h"
#import "BSViewController.h"
#import "ASIFormDataRequest.h"
#import "Constance.h"
#import "JMWhenTapped.h"
//#import "UIViewController+MJPopupViewController.h"
//#import "PupupViewController.h"
#import "GradientView.h"
#import "AFKPageFlipper.h"
@interface WBViewController ()

@end

@implementation WBViewController
@synthesize wb_id=_wb_id;
@synthesize bs_id = _bs_id;
@synthesize arrayData = _arrayData;
@synthesize order = _order;

-(void)setWb_id:(int)wb_id{
    _wb_id = wb_id;
}

-(void)setBs_id:(int)bs_id{
    _bs_id = bs_id;
}

-(void)setOrder:(int)order{
    _order = order;
}

- (void)setArrayData:(NSMutableArray *)arrayData{
    _arrayData = [[NSMutableArray alloc] init];
    _arrayData = arrayData;
}

- (NSInteger) numberOfPagesForPageFlipper:(AFKPageFlipper *)pageFlipper {
    return 8;
	
}


- (UIView *) viewForPage:(NSInteger) page inFlipper:(AFKPageFlipper *) pageFlipper {
	CGRect frame = self.view.bounds;
    UIView * newView = [[UIView alloc] initWithFrame:frame];
    
    NSLog(@"the page is %i", page);
    NSDictionary *dic_data = [_arrayData objectAtIndex:page-1];
    
    float ratio = [[dic_data objectForKey:@"ratio"] floatValue];
    int delta = 0;
    float image_x, image_width, image_height;
    if(ratio>=1.4375)
    {
        self.navigationController.navigationBar.barStyle = UIBarStyleBlackTranslucent;
        delta = 0;
        image_x = 0.0;
        image_width = 320.0;
        image_height = 320*ratio;
    }
    else if (ratio<1.4375 && ratio>=1.3){
        delta = -44;
        image_x = 0.0;
        image_width = 320.0;
        image_height = 320*ratio;
    }
    else if (ratio<1.3 && ratio>=1.125){
        delta = -44;
        image_height = 416.0;
        image_width = image_height/ratio;
        image_x = (320.0-image_width)/2;
    }
    else if (ratio<1.125 && ratio>=0.9375){
        delta = -44;
        image_height = 354.0;
        image_width = image_height/ratio;
        image_x = (320.0-image_width)/2;
    }
    else{
        delta = -44;
        image_height = 300.0;
        image_width = image_height/ratio;
        image_x = (320.0-image_width)/2;
    }
    CGRect image_frame = CGRectMake(image_x, 0, image_width, image_height);
    UIImageView *imageView = [[UIImageView alloc] initWithFrame:image_frame];
    [imageView setImage:[dic_data objectForKey:@"image"]];
    [newView addSubview:imageView];
    
    if(ratio>=1.125){
        CGRect gra_frame = CGRectMake(0, 300+delta, 320, 160);
        GradientView *gradientView = [[GradientView alloc] initWithFrame:gra_frame];
        [newView addSubview:gradientView];
    }
    if(ratio<1.125 && ratio>=0.937){
        CGRect gra_frame = CGRectMake(0, 300+delta, 320, 100);
        GradientView *gradientView = [[GradientView alloc] initWithFrame:gra_frame];
        [newView addSubview:gradientView];
    }
    
    CGRect label_frame = CGRectMake(10, 400+delta, 300, 1);
    UILabel *test = [[UILabel alloc] initWithFrame:label_frame];
    test.backgroundColor = [UIColor colorWithRed:0.5 green:0.5 blue:0.5 alpha:1.0];
    [newView addSubview:test];
    
    NSString *avatar_str = [dic_data objectForKey:@"bs_avatar"];
    CGRect avatar_frame = CGRectMake(10, 410+delta, 40, 40);
    UIImageView *avatar = [[UIImageView alloc] initWithFrame:avatar_frame];
    [avatar setImageWithURL:[[NSURL alloc] initWithString:avatar_str]];
    [newView addSubview:avatar];
    
    NSString *bs_name = [dic_data objectForKey:@"name"];
    CGRect name_label_frame  = CGRectMake(65, 410+delta, 200, 20);
    UILabel *bs_name_label = [[UILabel alloc] initWithFrame:name_label_frame];
    bs_name_label.backgroundColor = [UIColor clearColor];
    bs_name_label.text = bs_name;
    if(ratio>1.3){
        //bs_name_label.textColor = [UIColor colorWithRed:0.003 green:0.1098 blue:0.2863 alpha:1.0];
        bs_name_label.textColor = [UIColor whiteColor];
    }
    else{
        bs_name_label.textColor = [UIColor blackColor];
    }
    bs_name_label.font = [UIFont fontWithName:@"CourierNewPS-BoldMT" size:14];
    [newView addSubview:bs_name_label];
    
    NSString *body = [dic_data objectForKey:@"body"];
    //NSString *re_wb_name = [dic_data objectForKey:@"re_wb_name"];
    //NSString *re_wb_body = [dic_data objectForKey:@"re_wb_body"];
    //body = [[NSString alloc] initWithString:[NSString stringWithFormat:@"%@ // %@:%@", body, re_wb_name, re_wb_body]];
    CGRect body_frame = CGRectMake(25, 344+delta, 230, 50);
    UILabel *body_label = [[UILabel alloc] initWithFrame:body_frame];
    body_label.backgroundColor = [UIColor clearColor];
    body_label.font = [UIFont fontWithName:@"GillSans-Bold" size:14];
    body_label.numberOfLines = 3;
    if (ratio>0.9375) {
        //body_label.textColor = [UIColor colorWithRed:0.003 green:0.1098 blue:0.2863 alpha:1.0];
        body_label.textColor = [UIColor whiteColor];
    }
    else{
        body_label.textColor = [UIColor blackColor];
    }
    //body_label.textColor = [UIColor whiteColor];
    body_label.text = body;
    [newView addSubview:body_label];
    
    CGRect button_frame = CGRectMake(265, 344+delta, 40, 40);
    UIButton *add_to_wish = [[UIButton alloc] initWithFrame:button_frame];
    if (ratio>=0.9375) {
        [add_to_wish setBackgroundImage:[UIImage imageNamed:@"star4.png"] forState:UIControlStateNormal];
    }
    else{
        [add_to_wish setBackgroundImage:[UIImage imageNamed:@"star1.png"] forState:UIControlStateNormal];
    }
    [newView addSubview: add_to_wish];
    
    return newView;
}

- (void) loadView :(int)frontPage{
	[super loadView];
	self.view.autoresizesSubviews = YES;
	self.view.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
	
	flipper = [[AFKPageFlipper alloc] initWithFrame:self.view.bounds];
	flipper.autoresizingMask = UIViewAutoresizingFlexibleWidth | UIViewAutoresizingFlexibleHeight;
    [flipper setDataSource:self withPage:frontPage];
    [flipper setCurrentPage:frontPage];
	[self.view addSubview:flipper];
}

- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        
    }
    return self;
}

- (void)viewDidLoad
{
    //viewControlerStack = [[NSMutableArray alloc] initWithObjects:@"aaa", @"bbb", @"cccc", @"ddd", nil];
    NSLog(@"the order is %i", _order);
    [self loadView:_order+1];
    [super viewDidLoad];
    //self.view.frame= CGRectMake(0, 0, 300, 400);
}

- (void)viewDidUnload
{

    [self setArrayData:nil];
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (void)viewDidAppear:(BOOL)animated
{
    [super viewDidAppear:animated];
}

- (void)viewWillAppear:(BOOL)animated
{
    self.parentViewController.tabBarController.tabBar.hidden  = YES;
    [super viewWillAppear:animated];
}



- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

@end
