//
//  categViewController.m
//  puuten
//
//  Created by wang jialei on 12-9-23.
//
//

#import "categViewController.h"
#import "LoginViewController.h"
#import "JMWhentapped.h"
#import "LibViewController.h"
@interface categViewController ()<LoginViewControllerDelegate>

@end

@implementation categViewController
@synthesize selected_tag;
@synthesize login_or_not;


- (void)prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
{
    if ([segue.identifier isEqualToString:@"wb_categ"]) {
        LibViewController *lib = (LibViewController *)segue.destinationViewController;
        lib.categ = selected_tag;
    }
    if ([segue.identifier isEqualToString:@"login_beta"]) {
        LoginViewController *login = (LoginViewController *)segue.destinationViewController;
        login.delegate = self;
    }
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
	UIImage *img = [UIImage imageNamed:@"11.jpeg"];
    CGRect frame = CGRectMake(0, 0, img.size.width*460/img.size.height, 460);
    UIImageView *imgView = [[UIImageView alloc] initWithFrame:frame];
    [imgView setImage:img];
    [self.view addSubview:imgView];
    
    CGRect frame1 = CGRectMake(20, 20, 130,75);
    UILabel *label1 = [[UILabel alloc] initWithFrame:frame1];
    label1.backgroundColor =  [UIColor colorWithRed:0.2 green:0.4 blue:0.4 alpha:0.85];
    label1.text = @"美食";
    label1.textColor = [UIColor whiteColor];
    [self.view addSubview:label1];
    [label1 whenTapped:^{
        selected_tag = @"美食";
        [self performSegueWithIdentifier:@"wb_categ" sender:self];
    }];
    
    CGRect frame2 = CGRectMake(170, 20, 130,75);
    UILabel *label2 = [[UILabel alloc] initWithFrame:frame2];
    label2.backgroundColor =  [UIColor colorWithRed:0.2 green:0.4 blue:0.4 alpha:0.85];
    label2.text = @"饮品";
    label2.textColor = [UIColor whiteColor];
    [self.view addSubview:label2];
	[label2 whenTapped:^{
        selected_tag = @"饮品";
        [self performSegueWithIdentifier:@"wb_categ" sender:self];
    }];
}

- (void)viewDidAppear:(BOOL)animated
{
    if (!login_or_not) {
        [self performSegueWithIdentifier:@"login_beta" sender:self];
    }
    [super viewDidAppear:animated];
}

- (void)viewDidUnload
{
    [super viewDidUnload];
    // Release any retained subviews of the main view.
}

- (BOOL)shouldAutorotateToInterfaceOrientation:(UIInterfaceOrientation)interfaceOrientation
{
    return (interfaceOrientation == UIInterfaceOrientationPortrait);
}

- (void)loginViewController:(LoginViewController *)sender
               login_or_not:(int)userid
{
    self.login_or_not = YES;
    [self dismissModalViewControllerAnimated:YES];
}

@end
