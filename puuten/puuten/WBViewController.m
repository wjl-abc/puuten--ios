//
//  WBViewController.m
//  puuten
//
//  Created by wang jialei on 12-8-3.
//
//

#import "WBViewController.h"
#import "ASIFormDataRequest.h"
#import "Constance.h"
#import "BSViewController.h"
#import "JMWhenTapped.h"
#import "UIViewController+MJPopupViewController.h"
#import "PupupViewController.h"
#import "GradientView.h"
@interface WBViewController ()

@end

@implementation WBViewController
//@synthesize name;

@synthesize wb_id=_wb_id;
@synthesize avatar_url = _avatar_url;
@synthesize bs_id;
@synthesize img = _img;

- (void)setWb_id:(int)wb_id
{
    _wb_id = wb_id;
}

- (void)setAvatar_url:(NSURL *)avatar_url
{
    _avatar_url = avatar_url;
}

- (void)setImg:(UIImage *)img{
    _img = img;
}

- (void)loadData
{
    NSString *wb_url_string = [NSString stringWithFormat:@"/business/wb/%d/", _wb_id];
    NSURL *nsURL = [[NSURL alloc] initWithString:URL];
    NSURL *wbURL = [NSURL URLWithString:wb_url_string relativeToURL:nsURL];
    ASIFormDataRequest *_request=[ASIFormDataRequest requestWithURL:wbURL];
    __weak ASIFormDataRequest *request = _request;
    [request setPostValue:@"ios" forKey:@"mobile"];
    [request setCompletionBlock:^{
        NSData *responseData = [request responseData];
        NSError* error;
        NSDictionary* json = [NSJSONSerialization JSONObjectWithData:responseData options:kNilOptions error:&error];
        
        float ratio = [[json objectForKey:@"ratio"] floatValue];
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
       // NSURL *pic_url = [[NSURL alloc] initWithString:[json objectForKey:@"pic_url"]];
       // NSData *data = [[NSData alloc] initWithContentsOfURL:pic_url];
       // UIImage *image = [[UIImage alloc] initWithData:data];
        //self.view.layer.contents = (id)[image CGImage];
        //UIImage *image = [[UIImage alloc] initWithData:data];
        CGRect image_frame = CGRectMake(image_x, 0, image_width, image_height);
        UIImageView *imageView = [[UIImageView alloc] initWithFrame:image_frame];
        //[imageView setImage:image];
        [imageView setImage:_img];
        [self.view addSubview:imageView];
        if(ratio>=1.125){
            CGRect gra_frame = CGRectMake(0, 300+delta, 320, 160);
            GradientView *gradientView = [[GradientView alloc] initWithFrame:gra_frame];
            [self.view addSubview:gradientView];
        }
        if(ratio<1.125 && ratio>=0.937){
            CGRect gra_frame = CGRectMake(0, 300+delta, 320, 100);
            GradientView *gradientView = [[GradientView alloc] initWithFrame:gra_frame];
            [self.view addSubview:gradientView];
        }

        CGRect label_frame = CGRectMake(10, 400+delta, 300, 1);
        UILabel *test = [[UILabel alloc] initWithFrame:label_frame];
        test.backgroundColor = [UIColor colorWithRed:0.5 green:0.5 blue:0.5 alpha:1.0];
        [self.view addSubview:test];
        
        NSString *avatar_str = [json objectForKey:@"avatar_url"];
        CGRect avatar_frame = CGRectMake(10, 410+delta, 40, 40);
        UIImageView *avatar = [[UIImageView alloc] initWithFrame:avatar_frame];
        [avatar setImageWithURL:[[NSURL alloc] initWithString:avatar_str]];
        [self.view addSubview:avatar];
        
        NSString *bs_name = [json objectForKey:@"name"];
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
        [self.view addSubview:bs_name_label];
        
        NSString *body = [json objectForKey:@"body"];
        NSString *re_wb_name = [json objectForKey:@"re_wb_name"];
        NSString *re_wb_body = [json objectForKey:@"re_wb_body"];
        body = [[NSString alloc] initWithString:[NSString stringWithFormat:@"%@ // %@:%@", body, re_wb_name, re_wb_body]];
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
        [self.view addSubview:body_label];
        
        CGRect button_frame = CGRectMake(265, 344+delta, 40, 40);
        UIButton *add_to_wish = [[UIButton alloc] initWithFrame:button_frame];
        if (ratio>=0.9375) {
            [add_to_wish setBackgroundImage:[UIImage imageNamed:@"star4.png"] forState:UIControlStateNormal];
        }
        else{
            [add_to_wish setBackgroundImage:[UIImage imageNamed:@"star1.png"] forState:UIControlStateNormal];
        }
        [self.view addSubview: add_to_wish];
        
        [bs_name_label whenTapped:^{
            NSLog(@"business name has been tapped");
            //PupupViewController *pupView = [[PupupViewController alloc] initWithNibName:@"PupupViewController.xib" bundle:nil];
            //[self presentPopupViewController:pupView animationType:MJPopupViewAnimationFade];
        }];
        [avatar whenTapped:^{
            NSLog(@"business avatar has been tapped");
        }];
        [body_label whenTapped:^{
            NSLog(@"business body has been tapped");
        }];
        [imageView whenTapped:^{
            NSLog(@"imageView has been tapped");
        }];
        
    }];
    [request setFailedBlock:^{}];
    
    [request startAsynchronous];
}


- (id)initWithNibName:(NSString *)nibNameOrNil bundle:(NSBundle *)nibBundleOrNil
{
    self = [super initWithNibName:nibNameOrNil bundle:nibBundleOrNil];
    if (self) {
        // Custom initialization
    }
    return self;
}

- (void)viewDidLoad
{
    [super viewDidLoad];
    //self.view.backgroundColor = [UIColor greenColor];
    //self.view.layer.contents = (id)[[UIImage imageNamed:@"111.jpeg"] CGImage];
    //self.view.backgroundColor = [UIColor whiteColor];
    self.title = @"wb";
    //CGRect label_frame = CGRectMake(10, 400, 300, 1);
    //UILabel *test = [[UILabel alloc] initWithFrame:label_frame];
    //test.backgroundColor = [UIColor colorWithRed:0.5 green:0.5 blue:0.5 alpha:1.0];
    
    //CGRect avatar_frame = CGRectMake(10, 410, 30, 30);
    //UIImageView *avatar = [[UIImageView alloc] initWithFrame:avatar_frame];
    //[avatar setImageWithURL:_avatar_url];

    //[self.view addSubview:test];
    
    
    //[self.view addSubview:avatar];
}

- (void)viewDidUnload
{
//    [self setName:nil]
    [super viewDidUnload];
    [self setAvatar_url:nil];
    [self setImg:nil];
    // Release any retained subviews of the main view.
}

- (void)viewDidAppear:(BOOL)animated
{
   // ((UITabBarController *)self.parentViewController).tabBar.hidden = YES;
    [self loadData];
    [super viewDidAppear:animated];
}

- (void)viewWillAppear:(BOOL)animated
{
    self.parentViewController.tabBarController.tabBar.hidden  = YES;
    //[self.navigationController.navigationBar setAlpha:0];
    //self.navigationController.navigationBar.tintColor = [UIColor colorWithHue:1 saturation:0 brightness:1 alpha:0] ;
    //[self.navigationController.navigationBar setTintColor:[UIColor clearColor]];
    //self.navigationController.navigationBar.backgroundColor = [UIColor colorWithRed:0.3 green:0.94 blue:0.6 alpha:1.0];
    
}



- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}



@end
